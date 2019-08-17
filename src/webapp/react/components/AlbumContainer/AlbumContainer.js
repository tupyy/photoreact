import React from 'react'
import {GridList, PropTypes} from "@material-ui/core";
import Album from "../Album/Album";
import GridListTile from "@material-ui/core/GridListTile";

class AlbumContainer extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <GridList spacing={15} cellHeight={"auto"} cols={this.props.columns}>
                    {this.props.source.slice(0, this.props.rows * this.prop.column).map(album => (
                        <GridListTile key={album} cols={1}>
                            <Album
                                title = {album.title}
                                albumDate = {album.date}
                                albumDescription = {album.description}
                            />
                        </GridListTile>
                    ))}
                </GridList>
            </div>
        )
    }
}

AlbumContainer.prototype = {
    columns : PropTypes.number,
    rows: PropTypes.number,
    source: PropTypes.object
}

export default AlbumContainer;