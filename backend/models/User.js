const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  watchedMovies: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Movie' }],
  watchList: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Movie' }],
  isAdmin: { type: Boolean, default: false } // Ajout du champ isAdmin
});

module.exports = mongoose.model('User', userSchema);
