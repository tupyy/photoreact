import React, {useContext} from 'react';
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles} from "@material-ui/core";
import {Theme} from "@material-ui/core/styles/createMuiTheme";
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";
import combineStyles from "app/shared/util/combine-styles";

interface IOverview extends ITabComponent {
}

const useStyles = combineStyles(useTabComponentStyles, makeStyles( (theme: Theme) => ({
})));

export const Overview: React.SFC<IOverview> = (props: IOverview) => {
    const tabContext = useContext(TabContext);

    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={props.index !== tabContext.currentTab ? classes.hidden : classes.root}>
            Overview component
        </div>
    )
};

