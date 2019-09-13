import React, {useContext} from 'react';
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles, Theme} from "@material-ui/core";
import combineStyles from "app/shared/util/combine-styles";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";

interface IAlbumsTab extends ITabComponent {

}

const useStyles = combineStyles(useTabComponentStyles,makeStyles( (theme: Theme) => {

}));

const AlbumsTab: React.SFC<IAlbumsTab> = (props: IAlbumsTab) => {
    const tabContext = useContext(TabContext);

    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={props.index !== tabContext.currentTab ? classes.hidden : classes.root}>
            Album component
        </div>
    )
};

export default AlbumsTab;
