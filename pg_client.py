import logging
import psycopg2


class PgClient:
    def __init__(self, host, port, user, passwd, db):
        self.pg_cl = psycopg2.connect(host=host, port=port, database=db, user=user, password=passwd)

    def insert_sticker_pack(self, name, title, thumb, animated):
        with self.pg_cl:
            with self.pg_cl.cursor() as cur:
                query = "insert into sticker_pack(pack_name,title,thumb,animated,recommended,created_at) values(%s,%s,%s,%s,0, get_unix_timestamp()) ON CONFLICT (pack_name) DO UPDATE set thumb = EXCLUDED.thumb, created_at = get_unix_timestamp() "
                cur.execute(query, (name, title, thumb, animated))

    def set_recommended_pack(self, name):
        with self.pg_cl:
            with self.pg_cl.cursor() as cur:
                query = "update sticker_pack set recommended = 1 where pack_name=%s"
                cur.execute(query, (name,))

    def clear_recommended_pack(self):
        with self.pg_cl:
            with self.pg_cl.cursor() as cur:
                query = "update sticker_pack set recommended = 0"
                cur.execute(query)
