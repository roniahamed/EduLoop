"""
Database optimization migration for EduLoop
Adds performance indexes to improve query speed
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    
    dependencies = [
        ('questions', '0012_alter_question_options_question_q_group_idx_and_more'),
    ]
    
    operations = [
        # Add indexes for Group model
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_group_name_idx ON questions_group(name);",
            reverse_sql="DROP INDEX IF EXISTS questions_group_name_idx;"
        ),
        
        # Add indexes for Subject model  
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_subject_group_name_idx ON questions_subject(group_id, name);",
            reverse_sql="DROP INDEX IF EXISTS questions_subject_group_name_idx;"
        ),
        
        # Add indexes for Category model
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_category_subject_group_idx ON questions_category(subject_id, group_id);",
            reverse_sql="DROP INDEX IF EXISTS questions_category_subject_group_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_category_name_subject_idx ON questions_category(name, subject_id);",
            reverse_sql="DROP INDEX IF EXISTS questions_category_name_subject_idx;"
        ),
        
        # Add indexes for SubCategory model
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_subcategory_category_subject_idx ON questions_subcategory(category_id, subject_id);",
            reverse_sql="DROP INDEX IF EXISTS questions_subcategory_category_subject_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_subcategory_group_subject_idx ON questions_subcategory(group_id, subject_id);",
            reverse_sql="DROP INDEX IF EXISTS questions_subcategory_group_subject_idx;"
        ),
        
        # Add indexes for Question model (if not already present)
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_question_level_idx ON questions_question(level);",
            reverse_sql="DROP INDEX IF EXISTS questions_question_level_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_question_group_subject_category_idx ON questions_question(group_id, subject_id, category_id);",
            reverse_sql="DROP INDEX IF EXISTS questions_question_group_subject_category_idx;"
        ),
        
        # Add indexes for AccessToken model
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS users_accesstoken_active_created_idx ON users_accesstoken(is_active, created_at);",
            reverse_sql="DROP INDEX IF EXISTS users_accesstoken_active_created_idx;"
        ),
    ]