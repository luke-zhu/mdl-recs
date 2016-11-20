import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

const Similarities = new Mongo.Collection('similarities');

Meteor.methods({
  'similarities.similarTo': (shows) => {
    check(shows, Array);
    const rawSimilarities = Similarities.rawCollection();
    // console.log(rawSimilarities);
    const cursor = rawSimilarities.aggregate([{
      $match: { title_x: { $in: shows } },
    }, {
      $group: {
        _id: '$title_y',
        averageSimilarity: { $avg: '$similarity' },
      },
    }, {
      $sort: { averageSimilarity: -1 },
    }, {
      $limit: shows.length + 10,
    }, {
      $match: {
        _id: { $not: { $in: shows } },
      },
    }]);
    return cursor.toArray();
  },
});

export default Similarities;
