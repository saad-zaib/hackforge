// Hackforge Machine: eeebfddf108a523c
// Vulnerability: NoSQL Injection
// Run with: node app.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const mongoUrl = 'mongodb://localhost:27017';
const dbName = 'hackforge';

app.get('/', (req, res) => {
    res.send(`
        <html>
        <head><title>NoSQL Search</title></head>
        <body style="font-family: monospace; background: #1a1a2e; color: #eee; padding: 50px;">
            <h1>🔍 Search Users</h1>
            <form method="POST" action="/search">
                <input type="text" name="category" placeholder="Username" style="padding: 10px; width: 300px;">
                <button type="submit" style="padding: 10px 20px;">Search</button>
            </form>
        </body>
        </html>
    `);
});

app.post('/search', async (req, res) => {
    const category = req.body;
    
    MongoClient.connect(mongoUrl, async (err, client) => {
        if (err) return res.send('Error connecting to database');
        
        const db = client.db(dbName);
        const users = db.collection('users');
        
        // Vulnerable query - no sanitization
        const results = await users.find({ username: category }).toArray();
        
        res.send('<pre>' + JSON.stringify(results, null, 2) + '</pre>');
        client.close();
    });
});

app.listen(3000, () => console.log('Server running on port 3000'));
