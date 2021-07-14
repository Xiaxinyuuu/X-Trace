import sqlite3

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def initdb(self):
        try:
            conn = sqlite3.connect('videos.db')
            sql = '''CREATE TABLE videos
                   (
                   video_path    TEXT    NOT NULL,
                   video_date    TEXT    NOT NULL,
                   video_lenth     TEXT    NOT NULL,
                   threshold float
                   );'''  # 建表语句

            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.close()
            sql = '''
            SELECT * FROM videos;
            '''
        except:
            pass

    def insert_data(self, video_path, date,video_lenth,threshold):

        sql = 'insert into videos (video_path,video_date,video_lenth,threshold) values(?,?,?,?)'
        data = (video_path, date,video_lenth, threshold)
        self.cur.execute(sql, data)
        self.conn.commit()

    def search(self):
        sql = '''select * from videos;
        '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def delete_data(self,video_date):

        sql = 'delete from videos where video_date=?'
        self.cur.execute(sql,(video_date))
        self.conn.commit()

    def close_db(self):
        self.cur.close()
        self.conn.close()

