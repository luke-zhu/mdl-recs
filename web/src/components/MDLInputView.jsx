import React, { PropTypes } from 'react';
import TextField from 'material-ui/TextField';
import { connect } from 'react-redux';

import {
  showLoading,
  getMyShows,
  getSimilarShows
} from '../redux/actions';

const MDLInputView = ({ handleKeyPress }) => (
  <div>
    <TextField
      floatingLabelText="Enter your MDL username here."
      onKeyPress={handleKeyPress}
    />
  </div>
);

MDLInputView.propTypes = {
  handleKeyPress: PropTypes.func.isRequired,
};

const mapDispatchToProps = dispatch => ({
  handleKeyPress: (e) => {
    if (e.key === 'Enter') {
      console.log('Username entered');
      dispatch(showLoading());
      Meteor.call('mdl.getList', e.target.value, (error, result) => {
        if (error) console.error(error);
        else {
          console.log(result);
          dispatch(getMyShows(result));

          Meteor.call('similarities.similarTo',
            result.map(show => show.name),
            (error2, result2) => {
              if (error2) console.error(error2);
              else {
                console.log(result2);
                dispatch(getSimilarShows(result2));
              }
            }
          );
        }
      });
    }
  },
});

export default connect(null, mapDispatchToProps)(MDLInputView);
