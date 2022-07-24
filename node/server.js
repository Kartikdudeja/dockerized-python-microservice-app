// read environment variable from '.env' file
require('dotenv').config()

// import statements
const express = require('express')
const mongoose = require('mongoose')

// Mongo DB Connection
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true })
const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('Connected to Mongo Database.'))

// express instance of application
const app = express()

// allows app to accept data in json format
app.use(express.json())

// API Routers
const itemsRouter = require('./routes/items')
app.use('/items', itemsRouter)

app.listen(3000, () => console.log('Node Application Started.'))
