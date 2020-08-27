import logging
import psycopg2


class PgClient:
    def __init__(self, host, port, user, passwd, db):
        self.pg_cl = psycopg2.connect(host=host, port=port, database=db, user=user, password=passwd)

    def insert_sticker_pack(self, name, title, thumb, animated):
        query = "insert into sticker_pack(pack_name,title,thumb,animated,recommended,created_at) values('{0}','{1}','{2}',{3},0, get_unix_timestamp() ) ON CONFLICT (pack_name) DO UPDATE set thumb = '{2}', created_at = get_unix_timestamp() "\
            .format(name, title, thumb, str(animated))
        try:
            cur = self.pg_cl.cursor()
            cur.execute(query)
            self.pg_cl.commit()
            cur.close()
        except psycopg2.Error as e:
            logging.error(e.pgerror)
            return False
        return True

    def set_recommended_pack(self, name):
        query = "update sticker_pack set recommended = 1 where pack_name=%s"
        try:
            cur = self.pg_cl.cursor()
            cur.execute(query, (name,))
            self.pg_cl.commit()
            cur.close()
        except psycopg2.Error as e:
            logging.error(e.pgerror)
            return False
        return True
