const express = require("express");
const router = express.Router();
const {
  createItem,
  getAllItems,
  getItem,
  updateItem,
  deleteItem,
} = require("../controllers/itemController");
const authenticate = require("../middleware/auth");

// All item routes are protected
router.use(authenticate);

router.post("/", createItem);
router.get("/", getAllItems);
router.get("/:id", getItem);
router.put("/:id", updateItem);
router.delete("/:id", deleteItem);

module.exports = router;
