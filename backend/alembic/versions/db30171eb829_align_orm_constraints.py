"""align ORM constraints with the database

Revision ID: db30171eb829
Revises: eeb9279ed296
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "db30171eb829"
down_revision: Union[str, Sequence[str], None] = "eeb9279ed296"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    invalid_checks = {
        "admission_cycles.application_dates": connection.execute(
            sa.text(
                "SELECT EXISTS (SELECT 1 FROM admission_cycles "
                "WHERE application_end_date <= application_start_date)"
            )
        ).scalar(),
        "admission_cycles.academic_year": connection.execute(
            sa.text(
                "SELECT EXISTS (SELECT 1 FROM admission_cycles "
                "WHERE academic_year_end <= academic_year_start)"
            )
        ).scalar(),
        "program_intakes.application_dates": connection.execute(
            sa.text(
                "SELECT EXISTS (SELECT 1 FROM program_intakes "
                "WHERE application_open_at IS NOT NULL "
                "AND application_close_at IS NOT NULL "
                "AND application_close_at <= application_open_at)"
            )
        ).scalar(),
        "programs.delivery_mode": connection.execute(
            sa.text(
                "SELECT EXISTS (SELECT 1 FROM programs "
                "WHERE delivery_mode NOT IN "
                "('on_campus', 'online', 'hybrid'))"
            )
        ).scalar(),
    }

    violations = [
        name for name, exists in invalid_checks.items() if exists
    ]

    if violations:
        raise RuntimeError(
            "Cannot apply constraint migration; existing rows violate: "
            + ", ".join(violations)
        )

    op.drop_constraint(
        "ck_admission_cycle_application_dates",
        "admission_cycles",
        type_="check",
    )
    op.create_check_constraint(
        "ck_admission_cycle_application_dates",
        "admission_cycles",
        "application_end_date > application_start_date",
    )

    op.drop_constraint(
        "ck_admission_cycle_academic_year",
        "admission_cycles",
        type_="check",
    )
    op.create_check_constraint(
        "ck_admission_cycle_academic_year",
        "admission_cycles",
        "academic_year_end > academic_year_start",
    )

    op.drop_constraint(
        "ck_intake_application_dates",
        "program_intakes",
        type_="check",
    )
    op.create_check_constraint(
        "ck_intake_application_dates",
        "program_intakes",
        "application_open_at IS NULL OR "
        "application_close_at IS NULL OR "
        "application_close_at > application_open_at",
    )

    op.create_check_constraint(
        "ck_program_delivery_mode",
        "programs",
        "delivery_mode IN ('on_campus', 'online', 'hybrid')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_program_delivery_mode",
        "programs",
        type_="check",
    )

    op.drop_constraint(
        "ck_intake_application_dates",
        "program_intakes",
        type_="check",
    )
    op.create_check_constraint(
        "ck_intake_application_dates",
        "program_intakes",
        "application_open_at IS NULL OR "
        "application_close_at IS NULL OR "
        "application_open_at <= application_close_at",
    )

    op.drop_constraint(
        "ck_admission_cycle_academic_year",
        "admission_cycles",
        type_="check",
    )
    op.create_check_constraint(
        "ck_admission_cycle_academic_year",
        "admission_cycles",
        "academic_year_start <= academic_year_end",
    )

    op.drop_constraint(
        "ck_admission_cycle_application_dates",
        "admission_cycles",
        type_="check",
    )
    op.create_check_constraint(
        "ck_admission_cycle_application_dates",
        "admission_cycles",
        "application_start_date <= application_end_date",
    )