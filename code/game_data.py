import pygame
import sqlite3


class GameData:
    def __init__(self):
        # Kết nối database
        self.conn = sqlite3.connect("GameData.db")
        # Tạo bảng
        create_table = """CREATE TABLE IF NOT EXISTS Leaderboard (
        Rank INTEGER,
        Name TEXT NOT NULL,
        Score DOUBLE,
        Wave INTEGER)"""
        self.conn.execute(create_table)

    def insert_data(self, name, score, wave):
        insert_table = (
            "INSERT INTO Leaderboard (Name, Score, Wave) VALUES (:Name, :Score, :Wave)"
        )
        self.conn.execute(insert_table, {"Name": name, "Score": score, "Wave": wave})
        self.conn.commit()

        self.sort_data()

    def delete_data(self):
        # xóa dưx liệu
        delete_table = '''DELETE FROM Leaderboard'''
        self.conn.execute(delete_table)
        self.conn.commit()

    def get_data(self):
        # trả về dữ liệu
        select_table = '''SELECT * FROM Leaderboard'''
        data = self.conn.execute(select_table)
        self.conn.commit()
        return data
    
    def sort_data(self):
        self.conn.execute("SELECT * FROM Leaderboard ORDER BY Score DESC")
        sorted_data = self.conn.fetchall()
        #
        self.delete_data()
        #
        i = 0
        for row in sorted_data:
            row[0] = i + 1
            self.conn.execute("INSERT INTO players VALUES (?, ?, ?, ?)", row)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
