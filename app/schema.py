from __future__ import annotations

from .db import get_connection


EQUIPMENT_TABLES: dict[str, list[str]] = {
    "ecl760_daily": [
        "run_both_level_control",
        "machine_cleaning_dusting",
        "performed_rinse",
        "check_reagents_above_30",
        "check_consumables",
        "check_dw",
        "discard_liquid_waste",
        "discard_solid_waste",
        "cleaning_of_probe",
        "fill_cup",
        "check_di_clean_i",
        "check_sample_cup",
    ],
    "maglumi800_daily": [
        "prime_all",
        "performed_daily_maintenance",
        "light_check_alternate_day",
        "background_check_daily",
        "clean_analyzer",
        "check_consumables",
        "cuvette",
        "system_liquid_above_20",
        "check_starter",
        "empty_solid_waste",
        "empty_liquid_waste",
    ],
}


BASE_COLUMNS = """
    `id` int NOT NULL AUTO_INCREMENT,
    {check_columns}
    `datetime` varchar(225) NOT NULL,
    `documentedby` varchar(225) NOT NULL,
    `approvedby` varchar(225) NOT NULL DEFAULT 'Pending',
    `status` int NOT NULL DEFAULT '0',
    `verifiedby` varchar(225) NOT NULL DEFAULT '',
    `variftime` varchar(225) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`)
"""


def ensure_equipment_tables() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            for table, check_columns in EQUIPMENT_TABLES.items():
                check_sql = "".join(f"`{column}` varchar(10) NOT NULL DEFAULT '',\n    " for column in check_columns)
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS `{table}` ("
                    + BASE_COLUMNS.format(check_columns=check_sql)
                    + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
                )
                cur.execute(f"SHOW COLUMNS FROM `{table}`")
                existing = {str(row["Field"]) for row in cur.fetchall()}
                for column in check_columns:
                    if column not in existing:
                        cur.execute(
                            f"ALTER TABLE `{table}` "
                            f"ADD COLUMN `{column}` varchar(10) NOT NULL DEFAULT ''"
                        )
                for column, definition in {
                    "datetime": "varchar(225) NOT NULL",
                    "documentedby": "varchar(225) NOT NULL",
                    "approvedby": "varchar(225) NOT NULL DEFAULT 'Pending'",
                    "status": "int NOT NULL DEFAULT '0'",
                    "verifiedby": "varchar(225) NOT NULL DEFAULT ''",
                    "variftime": "varchar(225) NOT NULL DEFAULT ''",
                }.items():
                    if column not in existing:
                        cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")
        conn.commit()
