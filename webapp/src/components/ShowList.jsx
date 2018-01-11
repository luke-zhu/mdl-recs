import List, {ListItem, ListItemText} from 'material-ui/List';
import React from 'react';
import {connect} from 'react-redux';

import {selectShow} from '../redux/actions';

class ShowList extends React.Component {
  render() {
    const showViews = this.props.shows.slice(0, 5).map((e, i) => {
      const year = e._source.release_date.slice(0, 4);
      return (
          <ListItem
              button
              key={e._source.id}
              onClick={() => this.props.selectShow(i)}
          >
            <ListItemText
                primary={e._source.main_title}
                secondary={year}
            />
          </ListItem>
      );
    });
    return (
        <div>
          <List>
            {showViews}
          </List>
        </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    shows: state.shows,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    selectShow(index) {
      return dispatch(selectShow(index));
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ShowList);
