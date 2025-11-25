# from models.officer import Officer
# class OfficerAssignment:
#     @staticmethod
#     def assign_officer(db, category, city):
#         # 1. Match category, city, and only active officers
#         officer = (
#             db.query(Officer)
#             .filter(
#                 Officer.category_expertise == category,
#                 Officer.city == city,
#                 Officer.is_active == True
#             )
#             .order_by(Officer.current_load.asc())   # Lowest load first
#             .first()
#         )
#
#         # 2. If city-specific officer not found → match only category
#         if not officer:
#             officer = (
#                 db.query(Officer)
#                 .filter(
#                     Officer.category_expertise == category,
#                     Officer.is_active == True
#                 )
#                 .order_by(Officer.current_load.asc())
#                 .first()
#             )
#
#         return officer

# botree1/functions/officer_assignment.py
from models.officer import Officer
from sqlalchemy import func


class OfficerAssignment:
    @staticmethod
    def assign_officer(db, category, district, mandal=None, village_ward=None):
        """
        Assign officer based on:
        1. Category expertise (required match)
        2. Location hierarchy: village_ward → mandal → district
        3. Availability: is_active=True AND current_load < max_load
        4. Load balancing: lowest current_load first
        """

        available = db.query(Officer).all()
        for o in available:
            print("OFFICER:", o.name, o.category_expertise, o.district, o.mandal, o.village_ward)
        print("Searching for officer with:", category, district, mandal, village_ward)


        # Level 1: Exact match - village_ward + mandal + district + category
        if village_ward and mandal and district:
            officer = (
                db.query(Officer)
                # .filter(
                #     Officer.category_expertise == category,
                #     Officer.village_ward == village_ward,
                #     Officer.mandal == mandal,
                #     Officer.district == district,
                #     Officer.is_active == True,
                #     Officer.current_load < Officer.max_load
                # )
                .filter(
                    func.lower(Officer.category_expertise) == category.lower(),
                    func.lower(Officer.village_ward) == village_ward.lower(),
                    func.lower(Officer.mandal) == mandal.lower(),
                    func.lower(Officer.district) == district.lower(),
                    Officer.is_active == True,
                    Officer.current_load < Officer.max_load
                )
                .order_by(Officer.current_load.asc())
                .first()
            )
            if officer:
                return officer

        # Level 2: Mandal + district + category
        if mandal and district:
            officer = (
                db.query(Officer)
                .filter(
                    Officer.category_expertise == category,
                    Officer.mandal == mandal,
                    Officer.district == district,
                    Officer.is_active == True,
                    Officer.current_load < Officer.max_load
                )
                .order_by(Officer.current_load.asc())
                .first()
            )
            if officer:
                return officer

        # Level 3: District + category
        if district:
            officer = (
                db.query(Officer)
                .filter(
                    Officer.category_expertise == category,
                    Officer.district == district,
                    Officer.is_active == True,
                    Officer.current_load < Officer.max_load
                )
                .order_by(Officer.current_load.asc())
                .first()
            )
            if officer:
                return officer

        # Level 4: Any available officer with category (fallback)
        officer = (
            db.query(Officer)
            .filter(
                Officer.category_expertise == category,
                Officer.is_active == True,
                Officer.current_load < Officer.max_load
            )
            .order_by(Officer.current_load.asc())
            .first()
        )
        return officer
