// consumer listens for messages from RabbitMQ

// dependency
// npm install amqplib

// we open a connection and a channel, and declare the queue from which we're going to consume.
var amqp = require('amqplib/callback_api');
var request = require('request');

require('dotenv').config()
const QUEUE_URL = process.env.QUEUE_URL
const QUEUE_NAME = process.env.QUEUE_NAME

async function createApiCall(reqBody){

    var options = {
        'method': 'POST',
        'url': 'http://localhost:3000/items/',
        'headers': {
        'Content-Type': 'application/json'
    },
        
    body: reqBody
      
    };
    
    await request(options, function (error, response) {
        if (error) throw new Error(error);
        console.log(response.body);
    });
}

amqp.connect(QUEUE_URL , function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        var queue = QUEUE_NAME;
        
        channel.assertQueue(queue, {
            durable: false
        });

        // Since it will push us messages asynchronously, 
        // we provide a callback that will be executed when RabbitMQ pushes messages to our consumer.

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

        channel.consume(queue, function(msg) {
            console.log(" [x] Received '%s'; Calling CREATE Endpoint", msg.content.toString()); 
            console.log(msg.content.toString())
            createApiCall(msg.content.toString());

        }, {
            noAck: true
        });
    });
});