import operator
import uuid
from functools import reduce
from typing import Any

from pydantic import BaseModel, Field, create_model as pydantic_create_model

from app.core.logger import log
from app.plugin.module_ai.custom.form_schema import FormSchema


def resolve_output_schema(response_schema: dict[str, Any] | None) -> type[BaseModel] | None:
    if not isinstance(response_schema, dict):
        return None

    schema_key = response_schema.get("schema_key")
    if isinstance(schema_key, str):
        schema_model = _get_registered_schema(schema_key)
        if schema_model is not None:
            return schema_model
        log.warning(f"未找到预置结构: {schema_key}")
    ## todo: json_schema 来自 FormSchema.model_json_schema())
    json_schema = response_schema.get("json_schema")
    if isinstance(json_schema, dict):
        try:
            return _build_model_from_json_schema(
                schema=json_schema,
                model_name=f"UserResponseSchema{uuid.uuid4().hex[:8]}",
            )
        except Exception as e:
            log.error(f"json_schema解析失败，回退默认结构: {e!s}")

    return None


def _get_registered_schema(schema_key: str) -> type[BaseModel] | None:
    normalized_key = str(schema_key).strip().lower()
    if not normalized_key:
        return None
    schema_registry: dict[str, type[BaseModel]] = {
        "form_v1": FormSchema,
        "formschema": FormSchema,
        "form_schema": FormSchema,
    }
    return schema_registry.get(normalized_key)


def _build_model_from_json_schema(
        schema: dict[str, Any],
        model_name: str,
        depth: int = 0,
) -> type[BaseModel]:
    if depth > 6:
        raise ValueError("json_schema嵌套层级超过限制")

    schema_type = schema.get("type")
    if schema_type not in {"object", None}:
        raise ValueError("json_schema根节点必须是 object")

    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        raise ValueError("json_schema.properties不能为空")
    if len(properties) > 64:
        raise ValueError("json_schema字段数量超过限制")

    required = schema.get("required") or []
    required_set = {item for item in required if isinstance(item, str)}

    model_fields: dict[str, tuple[Any, Any]] = {}
    for field_name, field_schema in properties.items():
        if not isinstance(field_name, str) or not field_name.strip():
            raise ValueError("json_schema字段名无效")
        if not isinstance(field_schema, dict):
            raise ValueError(f"字段结构无效: {field_name}")

        field_type = _json_schema_to_python_type(
            schema=field_schema,
            model_name=f"{model_name}_{field_name}",
            depth=depth + 1,
        )
        is_required = field_name in required_set
        default_value = ... if is_required else None
        description = field_schema.get("description")

        if isinstance(description, str) and description.strip():
            model_fields[field_name] = (
                field_type,
                Field(default=default_value, description=description.strip()),
            )
        else:
            model_fields[field_name] = (field_type, default_value)

    if not model_fields:
        raise ValueError("json_schema中没有可用字段")

    return pydantic_create_model(model_name, **model_fields)


def _json_schema_to_python_type(
        schema: dict[str, Any],
        model_name: str,
        depth: int,
) -> Any:
    if depth > 6:
        raise ValueError("json_schema嵌套层级超过限制")

    if "anyOf" in schema and isinstance(schema["anyOf"], list):
        return _union_from_schema_list(
            schemas=schema["anyOf"],
            model_name=model_name,
            depth=depth + 1,
        )

    if "oneOf" in schema and isinstance(schema["oneOf"], list):
        return _union_from_schema_list(
            schemas=schema["oneOf"],
            model_name=model_name,
            depth=depth + 1,
        )

    schema_type = schema.get("type")
    nullable = False

    if isinstance(schema_type, list):
        normalized_types = [item for item in schema_type if isinstance(item, str)]
        nullable = "null" in normalized_types
        normalized_types = [item for item in normalized_types if item != "null"]
        if len(normalized_types) > 1:
            union_type = _union_from_type_names(
                type_names=normalized_types,
                schema=schema,
                model_name=model_name,
                depth=depth + 1,
            )
            return union_type | None if nullable else union_type
        schema_type = normalized_types[0] if normalized_types else None

    python_type = _single_json_schema_type_to_python_type(
        schema_type=schema_type,
        schema=schema,
        model_name=model_name,
        depth=depth + 1,
    )
    return python_type | None if nullable else python_type


def _single_json_schema_type_to_python_type(
        schema_type: Any,
        schema: dict[str, Any],
        model_name: str,
        depth: int,
) -> Any:
    if schema_type == "string":
        return str
    if schema_type == "integer":
        return int
    if schema_type == "number":
        return float
    if schema_type == "boolean":
        return bool
    if schema_type == "array":
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            item_type = _json_schema_to_python_type(
                schema=item_schema,
                model_name=f"{model_name}_item",
                depth=depth + 1,
            )
            return list[item_type]
        return list[Any]
    if schema_type == "object" or isinstance(schema.get("properties"), dict):
        return _build_model_from_json_schema(
            schema=schema,
            model_name=model_name,
            depth=depth + 1,
        )
    return Any


def _union_from_schema_list(
        schemas: list[Any],
        model_name: str,
        depth: int,
) -> Any:
    type_candidates: list[Any] = []
    nullable = False
    for index, item in enumerate(schemas):
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "null":
            nullable = True
            continue
        parsed_type = _json_schema_to_python_type(
            schema=item,
            model_name=f"{model_name}_{index}",
            depth=depth + 1,
        )
        type_candidates.append(parsed_type)

    if not type_candidates:
        return Any | None if nullable else Any

    union_type = _reduce_union_types(type_candidates)
    return union_type | None if nullable else union_type


def _union_from_type_names(
        type_names: list[str],
        schema: dict[str, Any],
        model_name: str,
        depth: int,
) -> Any:
    type_candidates = [
        _single_json_schema_type_to_python_type(
            schema_type=type_name,
            schema=schema,
            model_name=model_name,
            depth=depth + 1,
        )
        for type_name in type_names
    ]
    return _reduce_union_types(type_candidates)


def _reduce_union_types(type_candidates: list[Any]) -> Any:
    unique_types: list[Any] = []
    for item in type_candidates:
        if item not in unique_types:
            unique_types.append(item)
    if not unique_types:
        return Any
    if len(unique_types) == 1:
        return unique_types[0]
    return reduce(operator.or_, unique_types[1:], unique_types[0])
