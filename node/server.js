// read environment variable from '.env' file
require('dotenv').config()

// import statements
const express = require('express')
const mongoose = require('mongoose')

// Mongo DB Connection
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true })
const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('Connected to Mongo Database.\nWaiting for sometime before Starting the MQ Consumer...'))

// express instance of application
const app = express()

// allows app to accept data in json format
app.use(express.json())

// API Routers
const itemsRouter = require('./routes/items')
app.use('/items', itemsRouter)

app.listen(3000, () => console.log('Node Application Started.'))

// Run MQ Consumer after some wait
var delayInMilliseconds = process.env.WAIT_FOR_QUEUE_MILLI_SECONDS; // 1 second = 1000 milli seconds

setTimeout(function() {

    console.log('Starting Message Queue Consumer...')
    var fork = require('child_process').fork;
    var child = fork('./consumer');

}, delayInMilliseconds);
