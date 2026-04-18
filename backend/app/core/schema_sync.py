from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection
from sqlalchemy.schema import CreateColumn, CreateIndex, Index
from sqlalchemy.sql.schema import Column, MetaData, Table


def sync_missing_columns(connection: Connection, metadata: MetaData) -> list[dict[str, Any]]:
    """
    仅为已存在的数据表补齐缺失字段。

    注意：
    - 不处理字段修改
    - 不处理字段删除
    - 字段重命名会被视为新增字段，旧字段会被保留
    """
    inspector = inspect(connection)
    dialect = connection.dialect
    preparer = dialect.identifier_preparer
    actions: list[dict[str, Any]] = []

    for table in metadata.sorted_tables:
        if not inspector.has_table(table.name, schema=table.schema):
            continue

        existing_columns = {
            column_info["name"]
            for column_info in inspector.get_columns(table.name, schema=table.schema)
        }

        for column in table.columns:
            if column.name in existing_columns:
                continue

            can_add, reason = _can_auto_add_column(connection, table, column)
            if not can_add:
                actions.append(
                    {
                        "action": "skip",
                        "table": table.fullname,
                        "column": column.name,
                        "reason": reason,
                    }
                )
                continue

            column_sql = str(CreateColumn(column).compile(dialect=dialect))
            table_sql = preparer.format_table(table)
            connection.execute(text(f"ALTER TABLE {table_sql} ADD COLUMN {column_sql}"))
            existing_columns.add(column.name)
            actions.append(
                {
                    "action": "add",
                    "table": table.fullname,
                    "column": column.name,
                    "reason": None,
                }
            )

    return actions


def sync_missing_indexes(
        connection: Connection,
        metadata: MetaData,
        target_columns: set[tuple[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """
    仅补齐保守范围内的简单索引。

    默认只处理单列、非唯一索引；复杂索引与唯一索引交由 Alembic 管理。
    """
    inspector = inspect(connection)
    actions: list[dict[str, Any]] = []

    for table in metadata.sorted_tables:
        if not inspector.has_table(table.name, schema=table.schema):
            continue

        existing_index_names = {
            index_info["name"]
            for index_info in inspector.get_indexes(table.name, schema=table.schema)
        }

        for index in table.indexes:
            can_add, reason = _can_auto_add_index(index)
            column_names = [column.name for column in index.columns]

            if target_columns is not None:
                if len(column_names) != 1 or (table.fullname, column_names[0]) not in target_columns:
                    continue

            if index.name in existing_index_names:
                continue

            if not can_add:
                actions.append(
                    {
                        "action": "skip",
                        "table": table.fullname,
                        "index": index.name,
                        "reason": reason,
                    }
                )
                continue

            connection.execute(CreateIndex(index))
            existing_index_names.add(index.name)
            actions.append(
                {
                    "action": "add",
                    "table": table.fullname,
                    "index": index.name,
                    "reason": None,
                }
            )

    return actions


def _can_auto_add_column(
        connection: Connection,
        table: Table,
        column: Column[Any],
) -> tuple[bool, str | None]:
    """
    保守模式下，仅允许补齐风险较低的缺失字段。
    """
    if column.primary_key:
        return False, "主键字段不支持在启动时自动补齐"

    if column.computed is not None:
        return False, "计算字段不支持在启动时自动补齐"

    # if not column.nullable and column.server_default is None and _table_has_rows(connection, table):
    #     return False, "非空字段且无数据库默认值，自动补齐可能导致历史数据写入失败"

    return True, None


def _table_has_rows(connection: Connection, table: Table) -> bool:
    table_sql = connection.dialect.identifier_preparer.format_table(table)
    result = connection.execute(text(f"SELECT 1 FROM {table_sql} LIMIT 1"))
    return result.first() is not None


def _can_auto_add_index(index: Index) -> tuple[bool, str | None]:
    columns = list(index.columns)
    if len(columns) != 1:
        return False, "仅支持单列索引在启动时自动补齐"

    if index.unique:
        return False, "唯一索引不支持在启动时自动补齐"

    return True, None
