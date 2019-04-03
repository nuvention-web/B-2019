const router = require('express').Router();

router.get('/', (req, res, next) =>
  res.json({
    users: [
      {
        id: 1
      },
      {
        id: 2
      }
    ]
  })
);

module.exports = router;
