import {List, ListItem} from 'material-ui/List';
import React from 'react';
import {connect} from 'react-redux';

const styles = {
  marginBottom: 24,
  marginRight: 24,
};

class ShowList extends React.Component {
  render() {
    const showViews = this.props.shows.slice(0, 5).map((e) => {
      const year = e._source.release_date.slice(0, 4);
      return (
          <ListItem
              key={e._source.id}
              primaryText={e._source.main_title}
              secondaryText={year}
          />
      );
    });
    return (
        <div style={styles}>
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

export default connect(mapStateToProps)(ShowList);
