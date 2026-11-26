
"""Provision application users automatically on Supabase signup."""

from typing import Sequence, Union

from alembic import op

revision: str = "f4c8a2d91e63"
down_revision: Union[str, Sequence[str], None] = "db30171eb829"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the function executed whenever Supabase creates an auth user.
    op.execute("""
        CREATE OR REPLACE FUNCTION public.handle_new_user()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY DEFINER
        SET search_path = ''
        AS $$
        BEGIN
            INSERT INTO public.users (id)
            VALUES (NEW.id)
            ON CONFLICT (id) DO NOTHING;

            RETURN NEW;
        END;
        $$;
    """)

    # Attach the function to Supabase's auth.users table.
    op.execute("""
        CREATE TRIGGER on_auth_user_created
        AFTER INSERT ON auth.users
        FOR EACH ROW
        EXECUTE FUNCTION public.handle_new_user();
    """)

    # Provision application profiles for existing auth users too.
    op.execute("""
        INSERT INTO public.users (id)
        SELECT id
        FROM auth.users
        ON CONFLICT (id) DO NOTHING;
    """)

    # The trigger does not need to be directly callable by API users.
    op.execute("""
        REVOKE ALL ON FUNCTION public.handle_new_user() FROM PUBLIC;
    """)


def downgrade() -> None:
    op.execute("""
        DROP TRIGGER IF EXISTS on_auth_user_created
        ON auth.users;
    """)

    op.execute("""
        DROP FUNCTION IF EXISTS public.handle_new_user();
    """)
