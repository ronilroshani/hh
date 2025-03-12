import pyodbc
import logging
# تنظیمات لاگ‌گذاری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseError(Exception):
    """یک استثنای سفارشی برای مدیریت خطاهای پایگاه داده."""
    pass

class DatabaseManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """اتصال به پایگاه داده."""
        try:
            self.conn = pyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()
            logging.info("Database connection successful.")
        except pyodbc.Error as e:
            logging.error(f"Database connection error: {e}")
            raise DatabaseError("Unable to connect to the database.") from e

    def execute_query(self, query, params=(), commit=True):
        """اجرا کردن یک query با پارامترها، با امکان انتخاب تراکنش."""
        try:
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
            logging.info(f"Query executed successfully: {query},{params}")
        except pyodbc.Error as e:
            logging.error(f"Query execution error: {e}")
            raise DatabaseError("Error executing query.") from e

    def fetch_one_as_dict(self,cursor):
        columns = [column[0] for column in cursor.description]
        result = cursor.fetchone()
        if result:
            return dict(zip(columns, result))
        return None

    def fetch_ones(self, query, params=()):
        """اجرای کوئری و دریافت یک سطر از نتیجه."""
        try:
            self.cursor.execute(query, params)
            result = self.fetch_one_as_dict(self.cursor)
            if result:
                return result
            else:
                logging.info(f"No results found for query: {query} with params: {params}")
                return None
        except pyodbc.Error as e:
            logging.error(f"Query execution error: {e.args}")  # نمایش جزئیات بیشتر
            raise DatabaseError(f"Error fetching one result: {e.args[0]}") from e  # نمایش خطای دقیق‌تر

    def fetch_one(self, query, params=()):
        """اجرای کوئری و دریافت یک سطر از نتیجه."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                logging.info(f"No results found for query: {query}")
                return None
        except pyodbc.Error as e:
            logging.error(f"Query execution error: {e}")
            raise DatabaseError("Error fetching one result.") from e

    def fetch_all(self, query, params=()):
        """دریافت تمام نتایج یک query."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            raise DatabaseError("Error fetching data.") from e

    def fetch(self, query, params=()):
        try:
            query = "SELECT *  FROM EducationInfo"
            self.cursor.execute(query)
            self.cursor.execute(query, params)
            return [row.Gender for row in self.cursor.fetchall()]

            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            raise DatabaseError("Error fetching data.") from e


        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            raise DatabaseError("Error fetching data.") from e

    def __enter__(self):
        """پشتیبانی از مدیر زمینه."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """بستن اتصال پایگاه داده به طور خودکار."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    # تابع‌هایی برای دریافت مقادیر از جداول خارجی
    def fetch_gender_values(self):
        query = "SELECT GenderID,Gender  FROM Gender"
        self.cursor.execute(query)
        return [row.Gender for row in self.cursor.fetchall()]

    def fetch_skin_color_values(self):
        query = "SELECT SkinColourID,SkinColour FROM SkinColour"
        self.cursor.execute(query)
        return [row.SkinColour for row in self.cursor.fetchall()]

    def fetch_religion_values(self):
        query = "SELECT ReligionID, Religion FROM Religion"
        self.cursor.execute(query)
        return [row.Religion for row in self.cursor.fetchall()]

    def fetch_marital_status_values(self):
        query = "SELECT MaritalStatusID, MaritalStatus FROM MaritalStatus"
        self.cursor.execute(query)
        return [row.MaritalStatus for row in self.cursor.fetchall()]

    def fetch_blood_group_values(self):
        query = "SELECT BloodGroupID,BloodGroup FROM BloodGroup"
        self.cursor.execute(query)
        return [row.BloodGroup for row in self.cursor.fetchall()]

    def fetch_city_status_values(self):
        query = "SELECT CityName,CityName FROM City"
        self.cursor.execute(query)
        return [row.CityName for row in self.cursor.fetchall()]

    def fetch_eye_color_values(self):
        query = "SELECT EyeColorID,EyeColor FROM EyeColor"
        self.cursor.execute(query)
        return [row.EyeColor for row in self.cursor.fetchall()]

    def get_reward_by_national_code(self, national_code):
        query = "SELECT * FROM Reward WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            reward_data = {}
            for row in rows:
                reward_data = {
                    "NationalCode": row.NationalCode,
                    "RewardType": row.RewardType,
                    "RewardDate": row.RewardDate,
                    "Motivation": row.Motivation,
                    "RankAtTime": row.RankAtTime,
                    "Document": row.Document
                }
            return reward_data
        except Exception as e:
            logging.error(f"Error retrieving reward data for NationalCode {national_code}: {e}")
            raise

    def get_positive_seniority_by_national_code(self, national_code):
        query = "SELECT * FROM PositiveSeniority WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            positive_seniority_data = []
            for row in rows:
                positive_seniority_data.append({
                    "NationalCode": row.NationalCode,
                    "ServiceLocation": row.ServiceLocation,
                    "StartDate": row.StartDate,
                    "EndDate": row.EndDate,
                    "TotalServiceDuration": row.TotalServiceDuration,
                    "RankAtTimeOfService": row.RankAtTimeOfService,
                    "EmploymentStatus": row.EmploymentStatus,
                    "ServiceBreakDuration": row.ServiceBreakDuration,
                    "TerminationType": row.TerminationType,
                    "Document": row.Document
                })
            return positive_seniority_data
        except Exception as e:
            logging.error(f"Error retrieving positive seniority data for NationalCode {national_code}: {e}")
            raise


    def get_accident_by_national_code(self, national_code):
        query = "SELECT * FROM Accidents WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            accident_data = []
            for row in rows:
                accident_data.append({
                    "AccidentID": row.AccidentID,
                    "NationalCode": row.NationalCode,
                    "AccidentDate": row.AccidentDate,
                    "AccidentType": row.AccidentType,
                    "AccidentCause": row.AccidentCause,
                    "Document": row.Document
                })
            return accident_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise
    def get_language_by_national_code(self, national_code):
        query = "SELECT * FROM Languages WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            language_data = []
            for row in rows:
                language_data.append({
                    "LanguageID": row.LanguageID,
                    "NationalCode": row.NationalCode,
                    "LanguageType": row.LanguageType,
                    "LanguageDegree": row.LanguageDegree,
                    "LanguageCertificate": row.LanguageCertificate
                })
            return language_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise
    def get_millitary_by_national_code(self, national_code):
        query = "SELECT * FROM Millitary WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            language_data = []
            for row in rows:
                language_data.append({
                    "MillitaryID": row.MillitaryID,
                    "NationalCode": row.NationalCode,
                    "MillitaryTitle": row.MillitaryTitle,
                    "MillitaryLocation": row.MillitaryLocation,
                    "MillitaryStartDate": row.MillitaryStartDate,
                    "MillitaryEndDate": row.MillitaryEndDate,
                    "MillitaryDuration": row.MillitaryDuration,
                    "MillitaryMahdoodiyat": row.MillitaryMahdoodiyat,
                    "Document": row.Document,
                })
            return language_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise
    def get_clasic_by_national_code(self, national_code):
        query = "SELECT * FROM Classic WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            language_data = []
            for row in rows:
                language_data.append({
                    "ClassicID": row.ClassicID,
                    "NationalCode": row.NationalCode,
                    "ClassicTitle": row.ClassicTitle,
                    "ClassicField": row.ClassicField,
                    "ClassicLocation": row.ClassicLocation,
                    "ClassicStartDate": row.ClassicStartDate,
                    "ClassicEndDate": row.ClassicEndDate,
                    "ClassicDuration": row.ClassicDuration,
                    "Document": row.Document,
                })
            return language_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise
    def get_negative_seniority_by_national_code(self, national_code):
        query = "SELECT * FROM NegativeSeniority WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            negative_seniority_data = []
            for row in rows:
                negative_seniority_data.append({
                    "NationalCode": row.NationalCode,
                    "StartDate": row.StartDate,
                    "DurationDays": row.DurationDays,
                    "EndDate": row.EndDate,
                    "Typese": row.Typese,
                    "Document": row.Document,
                    "Notes": row.Notes
                })
            return negative_seniority_data
        except Exception as e:
            logging.error(f"Error retrieving negative seniority data for NationalCode {national_code}: {e}")
            raise
    def get_promotion_by_national_code(self, national_code):
        query = "SELECT * FROM PromotionFiles WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            accident_data = []
            for row in rows:
                accident_data.append({
                    "PromotionID": row.PromotionID,
                    "NationalCode": row.NationalCode,
                    "Document": row.Document,
                    "DegreeType": row.DegreeType,
                    "PromotionDate": row.PromotionDate,
                    "Degree": row.Degree
                })
            return accident_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise
    def get_mission_by_national_code(self, national_code):
        query = "SELECT * FROM MissionFile WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            positive_seniority_data = []
            for row in rows:
                positive_seniority_data.append({
                    "MissionDescription": row.MissionDescription,
                    "MissionStartDate": row.MissionStartDate,
                    "MissionEndDate": row.MissionEndDate,
                    "MissionDurationInMonths": row.MissionDurationInMonths,
                    "SendingOrganizationID": row.SendingOrganizationID,
                    "MissionDocument": row.MissionDocument,
                    "IsForeignMission": row.IsForeignMission,
                })
            return positive_seniority_data
        except Exception as e:
            logging.error(f"Error retrieving positive seniority data for NationalCode {national_code}: {e}")
            raise
    def get_forigen_mission_by_national_code(self, national_code):
        query = "SELECT * FROM MissionFile WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            positive_seniority_data = []
            for row in rows:
                positive_seniority_data.append({
                    "CountryID": row.CountryID,
                    "ForeignMissionStartDate": row.ForeignMissionStartDate,
                    "ForeignMissionEndDate": row.ForeignMissionEndDate,
                    "ForeignSendingOrganizationID": row.ForeignSendingOrganizationID,
                    "ForeignMissionDocument": row.ForeignMissionDocument,
                })
            return positive_seniority_data
        except Exception as e:
            logging.error(f"Error retrieving positive seniority data for NationalCode {national_code}: {e}")
            raise
    def get_job_by_national_code(self, national_code):
        query = "SELECT * FROM JobFiles WHERE NationalCode = ?"
        try:

            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()
            job_data = []
            for row in rows:
                job_data.append({
                    "JobFileID": row.JobFileID,
                    "NationalCode": row.NationalCode,
                    "AppointmentDoc": row.AppointmentDoc,
                    "AppointmentType": row.AppointmentType,
                    "AppointmentDate": row.AppointmentDate,
                    "State": row.State,
                    "AppointmentLoccationAppointment": row.AppointmentLoccationAppointment,
                    "JobType": row.JobType,
                    "OrganizationLocationMax": row.OrganizationLocationMax,
                    "JobTitle": row.JobTitle,
                    "Document": row.Document,
                    "SeparationType": row.SeparationType,
                    "SeparationDuration": row.SeparationDuration,
                    "EmployementState": row.EmployementState,
                    "Degree": row.Degree,
                    "EmployementDurationTotal": row.EmployementDurationTotal,
                    "EmployementStartDate": row.EmployementStartDate,
                    "EmploymentLocation": row.EmploymentLocation,
                })
            return job_data
        except Exception as e:
            logging.error(f"Error retrieving accident data for NationalCode {national_code}: {e}")
            raise

    def get_evaluation_by_national_code(self, national_code):
        """
        بازیابی اطلاعات ارزیابی کارمندان از جدول EmployeeEvaluations بر اساس کد ملی
        """
        query = "SELECT * FROM EmployeeEvaluation WHERE NationalCode = ?"
        try:
            self.cursor.execute(query, (national_code,))
            rows = self.cursor.fetchall()

            # دریافت اسامی ستون‌ها برای داینامیک‌سازی
            columns = [column[0] for column in self.cursor.description]

            evaluation_data = []
            for row in rows:
                # تبدیل هر ردیف به دیکشنری بر اساس ستون‌ها
                evaluation_data.append(dict(zip(columns, row)))

            return evaluation_data

        except Exception as e:
            logging.error(f"خطا در بازیابی اطلاعات ارزیابی برای کد ملی {national_code}: {e}")
            raise

    # def get_evaluation_by_national_code(self, national_code):
    #     query = "SELECT * FROM EmployeeEvaluation WHERE NationalCode = ?"
    #     try:
    #         self.cursor.execute(query, (national_code,))
    #         rows = self.cursor.fetchall()
    #         evaluation_data = []
    #         for row in rows:
    #             evaluation_data.append({
    #                 "NationalCode": row.NationalCode,
    #                 "Year": row.Year,
    #                 "Score": row.Score
    #             })
    #         return evaluation_data
    #     except Exception as e:
    #         logging.error(f"Error retrieving evaluation data for NationalCode {national_code}: {e}")
    #         raise

    def save_EmployeeEvaluationForm(self, employee_id, evaluation_date, score, comments):
        """
        این تابع اطلاعات ارزیابی یک کارمند را ذخیره یا به‌روزرسانی می‌کند.
        """
        # بررسی می‌کنیم که آیا ارزیابی برای این کارمند قبلاً وجود دارد یا خیر
        query_check = "SELECT COUNT(*) FROM EmployeeEvaluation WHERE EmployeeID = ?"
        try:
            count = self.fetch_one(query_check, (employee_id,))[0]

            if count > 0:
                # اگر ارزیابی قبلاً وجود دارد، آن را به‌روزرسانی می‌کنیم
                query_update = """
                UPDATE EmployeeEvaluation
                SET EvaluationDate = ?, Score = ?, Comments = ?
                WHERE EmployeeID = ?
                """
                self.execute_query(query_update, (evaluation_date, score, comments, employee_id), commit=True)
            else:
                # اگر ارزیابی وجود ندارد، یک ارزیابی جدید وارد می‌کنیم
                query_insert = """
                INSERT INTO EmployeeEvaluation (EmployeeID, EvaluationDate, Score, Comments)
                VALUES (?, ?, ?, ?)
                """
                self.execute_query(query_insert, (employee_id, evaluation_date, score, comments), commit=True)
        except Exception as e:
            self.logger.error(f"خطا در ذخیره یا به‌روزرسانی ارزیابی برای کارمند با شناسه {employee_id}: {e}")

    def get_EmployeeEvaluationForm(self, employee_id):
        """
        این تابع اطلاعات فرم ارزیابی یک کارمند را با استفاده از شناسه کارمند دریافت می‌کند.
        """
        query = """
        SELECT EvaluationDate, Score, Comments
        FROM EmployeeEvaluation
        WHERE EmployeeID = ?
        """
        try:
            result = self.fetch_one_as_dict(query, (employee_id,))
            if result:
                return result
            else:
                return None  # اگر هیچ ارزیابی برای کارمند وجود نداشته باشد
        except Exception as e:
            self.logger.error(f"خطا در دریافت ارزیابی برای کارمند با شناسه {employee_id}: {e}")
            return None

    def fetch_rewards(self, national_code):
        query = "SELECT * FROM Reward WHERE NationalCode = ?"
        self.cursor.execute(query, national_code)
        return self.cursor.fetchall()

    def fetch_disciplinary(self, national_code):
        query = "SELECT * FROM DisciplinaryActions WHERE NationalCode = ?"
        self.cursor.execute(query, national_code)
        return self.cursor.fetchall()

    def update_reward(self, reward_data):
        query = """
        UPDATE Rewards
        SET RewardType = ?, RewardDate = ?, Motivation = ?, RankAtTime = ?, Document = ?
        WHERE RewardID = ?
        """
        self.cursor.executemany(query, reward_data)
        self.conn.commit()

    def update_disciplinary(self, disciplinary_data):
        query = """
        UPDATE Disciplinary
        SET ActionType = ?, ActionDuration = ?, StartDate = ?, Document = ?, Rank = ?, Reason = ?, ApprovingAuthority = ?
        WHERE DisciplinaryID = ?
        """
        self.cursor.executemany(query, disciplinary_data)
        self.conn.commit()

    def create_reward(self, national_code, reward_data):
        query = """
        INSERT INTO Rewards (NationalCode, RewardType, RewardDate, Motivation, RankAtTime, Document)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.executemany(query, [(national_code, *row) for row in reward_data])
        self.conn.commit()

    def create_disciplinary(self, national_code, disciplinary_data):
        query = """
        INSERT INTO Disciplinary (NationalCode, ActionType, ActionDuration, StartDate, Document, Rank, Reason, ApprovingAuthority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.executemany(query, [(national_code, *row) for row in disciplinary_data])
        self.conn.commit()





