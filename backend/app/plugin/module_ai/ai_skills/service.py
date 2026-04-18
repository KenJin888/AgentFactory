import shutil
import zipfile
from pathlib import Path

import aiohttp

from app.config.path_conf import AI_SKILLS_DIR
from app.core.exceptions import CustomException


class AISkillsService:
    """
    AI技能管理服务层
    """

    @classmethod
    def _ensure_ai_skills_dir(cls):
        """确保AI技能目录存在"""
        if not AI_SKILLS_DIR.exists():
            AI_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _validate_skill_name(cls, name: str) -> Path:
        """
        验证技能名称，确保路径在AI技能目录内
        
        参数:
            name: 技能名称
            
        返回:
            Path对象
            
        异常:
            CustomException: 路径非法时抛出
        """
        cls._ensure_ai_skills_dir()
        
        target_path = AI_SKILLS_DIR.joinpath(name).resolve()
        ai_skills_dir_absolute = AI_SKILLS_DIR.resolve()
        
        if ai_skills_dir_absolute not in target_path.parents and target_path != ai_skills_dir_absolute:
            raise CustomException(msg="非法路径，只能操作AI技能目录内的文件")
        
        return target_path
    
    @classmethod
    def _handle_multilevel_directory(cls, skill_path: Path) -> None:
        """
        处理多层目录，定位到SKILL.md所在的层级
        
        参数:
            skill_path: 技能目录路径
        """
        # 查找SKILL.md文件
        skill_md_files = list(skill_path.rglob("SKILL.md"))
        
        if not skill_md_files:
            # 没有找到SKILL.md文件，直接返回
            return
        
        # 获取SKILL.md所在的目录
        skill_md_dir = skill_md_files[0].parent
        
        # 如果SKILL.md不在skill_path根目录，则需要移动内容
        if skill_md_dir != skill_path:
            # 移动skill_md_dir中的所有内容到skill_path
            for item in skill_md_dir.iterdir():
                target_item = skill_path.joinpath(item.name)
                # 如果目标已存在，先删除
                if target_item.exists():
                    if target_item.is_file():
                        target_item.unlink()
                    elif target_item.is_dir():
                        for subitem in target_item.rglob("*"):
                            if subitem.is_file():
                                subitem.unlink()
                            elif subitem.is_dir():
                                subitem.rmdir()
                        target_item.rmdir()
                # 移动文件或目录
                item.rename(target_item)
            
            # 删除空目录
            current_dir = skill_md_dir
            while current_dir != skill_path:
                parent_dir = current_dir.parent
                current_dir.rmdir()
                current_dir = parent_dir
                # 检查父目录是否为空
                if len(list(current_dir.iterdir())) > 0:
                    break

    @classmethod
    def _get_skill_description(cls, skill_md_path: Path) -> str:
        if not skill_md_path.exists():
            return ""

        content = skill_md_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        if not lines or lines[0].strip() != "---":
            return ""

        for line in lines[1:]:
            stripped_line = line.strip()
            if stripped_line == "---":
                break
            if stripped_line.startswith("description:"):
                description = stripped_line.split(":", 1)[1].strip()
                if (
                    len(description) >= 2
                    and description[0] == description[-1]
                    and description[0] in {'"', "'"}
                ):
                    description = description[1:-1]
                return description

        return ""

    @classmethod
    async def create_skill(cls, name: str, file=None, url: str = None) -> dict:
        """
        创建技能
        
        参数:
            name: 技能名称
            file: 上传的文件对象
            url: 技能zip包的下载地址
            
        返回:
            操作结果
        """
        skill_path = cls._validate_skill_name(name)
        
        if skill_path.exists():
            raise CustomException(msg="技能已存在")
        
        # 方式1：上传文件夹
        if file and file.filename is None:
            # 处理文件夹上传
            skill_path.mkdir(parents=True, exist_ok=True)
            # 这里需要处理文件夹上传的逻辑，暂时跳过
            return {"message": "技能创建成功"}
        
        # 方式2：上传zip压缩包
        elif file and file.filename and file.filename.endswith('.zip'):
            skill_path.mkdir(parents=True, exist_ok=True)
            content = await file.read()
            zip_path = skill_path.joinpath(f"{name}.zip")
            zip_path.write_bytes(content)
            
            # 解压zip文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(skill_path)
            
            # 删除zip文件
            zip_path.unlink()
            
            # 处理多层目录，定位到SKILL.md所在的层级
            cls._handle_multilevel_directory(skill_path)
            
            return {"message": "技能创建成功"}
        
        # 方式3：通过url下载zip
        elif url:
            skill_path.mkdir(parents=True, exist_ok=True)
            zip_path = skill_path.joinpath(f"{name}.zip")
            
            # 下载zip文件
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise CustomException(msg="下载zip文件失败")
                    content = await response.read()
                    zip_path.write_bytes(content)
            
            # 解压zip文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(skill_path)
            
            # 删除zip文件
            zip_path.unlink()
            
            # 处理多层目录，定位到SKILL.md所在的层级
            cls._handle_multilevel_directory(skill_path)
            
            return {"message": "技能创建成功"}
        
        else:
            raise CustomException(msg="请提供文件或url")

    @classmethod
    def delete_skill(cls, name: str) -> dict:
        """
        删除技能
        
        参数:
            name: 技能名称
            
        返回:
            操作结果
        """
        skill_path = cls._validate_skill_name(name)
        
        if not skill_path.exists():
            raise CustomException(msg="技能不存在")
        
        if not skill_path.is_dir():
            raise CustomException(msg="不是有效的技能目录")
        
        # 删除目录
        shutil.rmtree(skill_path)
        
        return {"message": "技能删除成功"}

    @classmethod
    def get_skill_detail(cls, name: str) -> dict:
        """
        获取技能详情
        
        参数:
            name: 技能名称
            
        返回:
            技能详情
        """
        skill_path = cls._validate_skill_name(name)
        
        if not skill_path.exists():
            raise CustomException(msg="技能不存在")
        
        skill_md_path = skill_path.joinpath("SKILL.md")
        
        if not skill_md_path.exists():
            raise CustomException(msg="SKILL.md文件不存在")
        
        content = skill_md_path.read_text(encoding="utf-8")
        
        return {"content": content}

    @classmethod
    def update_skill(cls, name: str, content: str) -> dict:
        """
        更新技能
        
        参数:
            name: 技能名称
            content: 新内容
            
        返回:
            操作结果
        """
        skill_path = cls._validate_skill_name(name)
        
        if not skill_path.exists():
            raise CustomException(msg="技能不存在")
        
        skill_md_path = skill_path.joinpath("SKILL.md")
        
        if not skill_md_path.exists():
            raise CustomException(msg="SKILL.md文件不存在")
        
        skill_md_path.write_text(content, encoding="utf-8")
        
        return {"message": "技能更新成功"}

    @classmethod
    def list_skills(cls) -> dict:
        """
        列出技能列表
        
        返回:
            技能列表
        """
        cls._ensure_ai_skills_dir()
        
        skills = []
        descriptions = []
        
        for item in AI_SKILLS_DIR.iterdir():
            if item.is_dir():
                skill_md_path = item.joinpath("SKILL.md")
                skills.append({"name": item.name, "description": cls._get_skill_description(skill_md_path)})
        
        return {"skills": skills}
