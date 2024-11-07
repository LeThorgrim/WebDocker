import express from 'express';
import pkg from 'pg';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

const { Pool } = pkg;
const app = express();
const port = 8001;

// Set up PostgreSQL connection using environment variables
const pool = new Pool({
    user: process.env.DATABASE_USER,
    host: process.env.DATABASE_HOST,
    database: process.env.DATABASE_NAME,
    password: process.env.DATABASE_PASSWORD,
    port: process.env.DATABASE_PORT,
  });

// Middleware to parse URL-encoded data from the form
app.use(express.urlencoded({ extended: true }));

// Serve static files from the public folder
app.use(express.static(path.join(process.cwd(), 'public')));

// Handle form submission
app.post('/check-user', async (req, res) => {
  const { username } = req.body;

  try {
    const result = await pool.query('SELECT * FROM "auth_user" WHERE username = $1', [username]);
    if (result.rows.length > 0) {
      res.send(`Username "${username}" exists in the database.`);
    } else {
      res.send(`Username "${username}" does not exist in the database.`);
    }
  } catch (err) {
    console.error(err);
    res.status(500).send('Database error occurred');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
