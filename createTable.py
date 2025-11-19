import asyncio
from database.CRUD import createTable


async def main():
    schema = {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "report_name": "VARCHAR(255) NOT NULL",
        "description": "TEXT",
        "company_id": "UUID NOT NULL",
        "user_id": "UUID NOT NULL",
        "actuals_data_file_path": "TEXT",
        "custom_data_file_path": "TEXT",
        "company_logo_path": "TEXT",
        "currency": "VARCHAR(50)",
        "created_on": "TIMESTAMP DEFAULT now()",
        "updated_on": "TIMESTAMP DEFAULT now()",
        "created_by": "UUID",
        "updated_by": "UUID",
        "__constraints__": [
            "FOREIGN KEY (company_id) REFERENCES master_company(id) ON DELETE CASCADE",
            "FOREIGN KEY (user_id) REFERENCES master_user(id) ON DELETE CASCADE",
            "FOREIGN KEY (created_by) REFERENCES master_user(id) ON DELETE SET NULL",
            "FOREIGN KEY (updated_by) REFERENCES master_user(id) ON DELETE SET NULL",
        ],
    }

    #     {
    #         "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    #         "user_id": "UUID NOT NULL",
    #         "company_name": "VARCHAR(255) NOT NULL",
    #         "industry": "VARCHAR(255)",
    #         "description": "TEXT",
    #         "created_on": "TIMESTAMP DEFAULT now()",
    #         "updated_on": "TIMESTAMP DEFAULT now()",
    #         "created_by": "UUID",
    #         "updated_by": "UUID",
    #         "__constraints__": [
    #             "FOREIGN KEY (user_id) REFERENCES master_user(id) ON DELETE CASCADE",
    #             "FOREIGN KEY (created_by) REFERENCES master_user(id) ON DELETE SET NULL",
    #             "FOREIGN KEY (updated_by) REFERENCES master_user(id) ON DELETE SET NULL"
    #         ]
    # }
    #     {
    #     "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    #     "role_id": "UUID NOT NULL",
    #     "user_id": "UUID NOT NULL",
    #     "__constraints__": [
    #         "FOREIGN KEY (role_id) REFERENCES master_role(id) ON DELETE CASCADE",
    #         "FOREIGN KEY (user_id) REFERENCES master_user(id) ON DELETE CASCADE",
    #         "FOREIGN KEY (created_by) REFERENCES master_user(id) ON DELETE SET NULL",
    #         "FOREIGN KEY (updated_by) REFERENCES master_user(id) ON DELETE SET NULL",
    #         "UNIQUE (role_id, user_id)"
    #     ]
    # }

    #     {
    #     "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    #     "role_id": "UUID NOT NULL",
    #     "user_id": "UUID NOT NULL",
    #     "__constraints__": [
    #         "FOREIGN KEY (role_id) REFERENCES master_role(id) ON DELETE CASCADE",
    #         "FOREIGN KEY (user_id) REFERENCES master_user(id) ON DELETE CASCADE",
    #         "FOREIGN KEY (created_by) REFERENCES master_user(id) ON DELETE SET NULL",
    #         "FOREIGN KEY (updated_by) REFERENCES master_user(id) ON DELETE SET NULL",
    #         "UNIQUE (role_id, user_id)"
    #     ]
    # }

    result = await createTable("master_report", schema)
    print(result)


asyncio.run(main())

# Role Permission Table
# {
#     "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#     "role_id": "UUID NOT NULL",
#     "permission_id": "UUID NOT NULL",
#     "__constraints__": [
#         "UNIQUE (role_id, permission_id)",
#         "FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE",
#         "FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE"
#     ]
# }


# Permission Table
# {
#         "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#         "name": "VARCHAR(50) NOT NULL",
#         "description": "VARCHAR(100) "
#     }

# Role Table
# {
#         "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#         "name": "VARCHAR(50) NOT NULL",
#         "description": "VARCHAR(100) "
#     }


# User Info
# {
#         "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#         "first_name": "VARCHAR(100) NOT NULL",
#         "last_name": "VARCHAR(100) ",
#         "email": "VARCHAR(255) UNIQUE NOT NULL",
#         "password": "TEXT NOT NULL",
#         "is_active": "BOOLEAN DEFAULT TRUE",
#         "last_login": "TIMESTAMP",
#         "is_deleted":"BOOLEAN DEFAULT FALSE",
#         "created_on": "TIMESTAMP DEFAULT now()",
#         "updated_on": "TIMESTAMP DEFAULT now()",
#         "created_by": "UUID",
#         "updated_by": "UUID",
#         "__constraints__": [
#             "FOREIGN KEY (created_by) REFERENCES user_info(id) ON DELETE SET NULL",
#             "FOREIGN KEY (updated_by) REFERENCES user_info(id) ON DELETE SET NULL"
#         ]
# }

# User Role

# {
#     "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#     "role_id": "UUID NOT NULL",
#     "user_id": "UUID NOT NULL",
#     "__constraints__": [
#         "FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE CASCADE",
#         "FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE",
#         "FOREIGN KEY (created_by) REFERENCES user_info(id) ON DELETE SET NULL",
#         "FOREIGN KEY (updated_by) REFERENCES user_info(id) ON DELETE SET NULL",
#         "UNIQUE (role_id, user_id)"
#     ]
# }

# Company
# {
#         "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
#         "user_id": "UUID NOT NULL",
#         "name": "VARCHAR(255) NOT NULL",
#         "industry": "VARCHAR(255)",
#         "description": "TEXT",
#         "created_on": "TIMESTAMP DEFAULT now()",
#         "updated_on": "TIMESTAMP DEFAULT now()",
#         "created_by": "UUID",
#         "updated_by": "UUID",
#         "__constraints__": [
#             "FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE",
#             "FOREIGN KEY (created_by) REFERENCES user_info(id) ON DELETE SET NULL",
#             "FOREIGN KEY (updated_by) REFERENCES user_info(id) ON DELETE SET NULL"
#         ]
# }
