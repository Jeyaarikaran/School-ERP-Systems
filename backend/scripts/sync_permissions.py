"""Idempotent script to sync the permissions catalog and system roles to the database."""

import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.permissions.catalog import CATALOG
from app.permissions.templates import SYSTEM_ROLES
from app.models.rbac import Permission, Role, RolePermission
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sync():
    db: Session = SessionLocal()
    try:
        logger.info("Starting permission sync...")
        
        # 1. Upsert Permissions
        existing_perms = {p.name: p for p in db.query(Permission).all()}
        for p_def in CATALOG:
            if p_def.name not in existing_perms:
                perm = Permission(name=p_def.name, module=p_def.module, description=p_def.description)
                db.add(perm)
                logger.info(f"Added permission: {p_def.name}")
            else:
                perm = existing_perms[p_def.name]
                if perm.description != p_def.description or perm.module != p_def.module:
                    perm.description = p_def.description
                    perm.module = p_def.module
                    logger.info(f"Updated permission: {p_def.name}")
                    
        db.flush()
        
        # 2. Re-map strings to DB IDs
        perm_map = {p.name: p.id for p in db.query(Permission).all()}
        
        # 3. Upsert System Roles
        existing_roles = {r.name: r for r in db.query(Role).filter(Role.is_system == True).all()}
        
        for role_name, perm_list in SYSTEM_ROLES.items():
            if role_name not in existing_roles:
                role = Role(name=role_name, is_system=True, description=f"System generated {role_name}")
                db.add(role)
                db.flush()
                logger.info(f"Added role: {role_name}")
            else:
                role = existing_roles[role_name]
                
            # Sync role permissions
            current_role_perms = {rp.permission_id for rp in db.query(RolePermission).filter_by(role_id=role.id).all()}
            target_role_perms = {perm_map[p] for p in perm_list if p in perm_map}
            
            # Add missing
            for p_id in (target_role_perms - current_role_perms):
                db.add(RolePermission(role_id=role.id, permission_id=p_id))
                
            # Remove revoked
            for p_id in (current_role_perms - target_role_perms):
                db.query(RolePermission).filter_by(role_id=role.id, permission_id=p_id).delete()
                
            logger.info(f"Synced permissions for role: {role_name}")
            
        db.commit()
        logger.info("Sync completed successfully.")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Sync failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    sync()
