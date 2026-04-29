from database.DB_connect import DBConnect
from model.situazione import Situazione

class MeteoDao:
    def __init__(self):
        raise RuntimeError('Do not create an instance, use the class methods!')

    @staticmethod
    def run_query(query, params=None, as_dictionary=False):
        cnx = DBConnect.get_connection()
        if cnx is None:
            raise RuntimeError('Database connection failed')

        with cnx.cursor(dictionary = as_dictionary) as cursor:
            cursor.execute(query, params or ())
            results = cursor.fetchall()

        cnx.close()
        return results

    @staticmethod
    def get_situazioni_mese(mese):
        query = """
        SELECT s.Localita, s.Data, s.Umidita
        FROM situazione s 
        where MONTH(s.`Data`) = %s
            and DAY(s.`Data`) < 16
        ORDER BY s.Data, s.Localita
        """
        data = MeteoDao.run_query(query, (mese,), as_dictionary=True)
        result = []
        for row in data:
            result.append(Situazione(row["Localita"],
                                     row["Data"],
                                     row["Umidita"]))
        return result

    @staticmethod
    def get_umidita_media_mese(mese):
        query = """
        SELECT 
        DISTINCT s.Localita,
        MONTH(s.`Data`) AS Mese,
        AVG(s.Umidita) AS Avg_umidita
        from situazione s 
        where MONTH(s.`Data`) = %s
        GROUP BY Localita, MONTH(s.`Data`)
        """
        return MeteoDao.run_query(query, (mese,), as_dictionary=True)

