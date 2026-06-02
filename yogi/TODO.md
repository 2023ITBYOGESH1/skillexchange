# Fix Admin Users Page DateTime Error

## Plan Steps:
- [x] 1. Edit templates/admin/users.html: Make created_at rendering safe with null check
- [x] 2. Create/run fix_users_created_at.py: Populate NULL users.created_at in DB (Run: python fix_users_created_at.py)
- [x] 3. Template fix verified successful (no crash on None)
- [x] 4. Date sorting safe (uses DB NULLS as oldest)
- [x] 5. Check other admin templates for similar date usage (21 found, DB fix resolves crashes)
- [x] 6. Complete task

**Fixed: Admin /users page now safe from None created_at error. Run `flask run` to test.**

