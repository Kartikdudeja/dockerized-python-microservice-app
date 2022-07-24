const express = require('express')
const router = express.Router()

// import database schema 
const Item = require('../models/item')

// Get All
router.get('/', async (req, res) => {
    console.log('get all request received, querying mongo db')
    try {
        console.log('db query succedded')
        const items =  await Item.find()
        res.json(items)
    } catch (err) {
        console.log('error occured while retreiving data from db.')
        res.status(500).json({ message: err.message })
    }
});

// Get One
router.get('/:id', getItem, (req, res) => {
    console.log('get one request for the id:', req.params.id)
    res.json(res.item)
}); 

// Create One
router.post('/', async (req, res) => {
    console.log('create request received')
    const item = new Item({
        key: req.body.key,
        value: req.body.value
    })
    try {
        const newItem = await item.save()
        res.status(201).json(newItem)
        console.log('new item successfully added in the db')
    } catch (err) {
        console.log('error occured while creating the new item')
        res.status(400).json({ message: err.message })
    }
});

// Update One
router.patch('/:id', getItem, async(req, res) => {
    console.log('update request for the id:', req.params.id)
    if (req.body.key != null) {
        res.item.name = req.body.key
    }
    if (req.body.value != null) {
        res.item.value = req.body.value
    }
    
    try {
        const updatedItem = await res.item.save()
        console.log('update request was successful')
        res.json(updatedItem)
    } catch (err) {
        console.log('some error occured!')
        res.status(400).json({ message: err.message })
    }
});

// Delete One
router.delete('/:id', getItem, async (req, res) => {
    console.log('delete request for the id:', req.params.id)
    try {
        await res.item.remove()
        console.log('Item Deleted')
        res.json({ message: 'Item Deleted' })
    } catch (err) {
        console.log('some error occured!')
        res.status(500).json({ message: err.message })
    }
});

async function getItem(req, res, next) {
    let item
    try {
      item = await Item.findById(req.params.id)
      if (item == null) {
        console.log('data not found')
        return res.status(404).json({ message: 'Cannot find data' })
      }
    } catch (err) {
      console.log('some error occured!')
      return res.status(500).json({ message: err.message })
    }
  
    res.item = item
    next()
  }  

module.exports = router