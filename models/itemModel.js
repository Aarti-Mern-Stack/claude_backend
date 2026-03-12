const pool = require("../config/db");

const Item = {
  async create(title, description, userId) {
    const [result] = await pool.query(
      "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)",
      [title, description, userId]
    );
    return result;
  },

  async findAll(userId) {
    const [rows] = await pool.query(
      "SELECT * FROM items WHERE user_id = ? ORDER BY created_at DESC",
      [userId]
    );
    return rows;
  },

  async findById(id, userId) {
    const [rows] = await pool.query(
      "SELECT * FROM items WHERE id = ? AND user_id = ?",
      [id, userId]
    );
    return rows[0];
  },

  async update(id, title, description, userId) {
    const [result] = await pool.query(
      "UPDATE items SET title = ?, description = ? WHERE id = ? AND user_id = ?",
      [title, description, id, userId]
    );
    return result;
  },

  async delete(id, userId) {
    const [result] = await pool.query(
      "DELETE FROM items WHERE id = ? AND user_id = ?",
      [id, userId]
    );
    return result;
  },
};

module.exports = Item;
