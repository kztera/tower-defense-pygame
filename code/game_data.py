import pygame
import sqlite3


class GameData:
    def __init__(self):
        # Kết nối database
        self.conn = sqlite3.connect("GameData.db")
        # Tạo bảng
        create_table = """CREATE TABLE IF NOT EXISTS Leaderboard (
        Name TEXT NOT NULL,
        Score DOUBLE,
        Wave INTEGER)"""
        self.conn.execute(create_table)

    def insert_data(self, name, score, wave):
        # thêm dữ liệu
        insert_table = (
            "INSERT INTO Leaderboard (Name, Score, Wave) VALUES (:Name, :Score, :Wave)"
        )
        self.conn.execute(insert_table, {"Name": name, "Score": score, "Wave": wave})
        self.conn.commit()

    def get_data(self):
        # trả về dữ liệu
        select_table = '''SELECT * FROM Leaderboard ORDER BY Score DESC LIMIT 10'''
        data = self.conn.execute(select_table)
        self.conn.commit()
        return data

    def __del__(self):
        self.conn.close()

