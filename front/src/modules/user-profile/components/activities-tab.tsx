import React, {useContext} from 'react';
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles} from "@material-ui/core";
import {Theme} from "@material-ui/core/styles/createMuiTheme";
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import combineStyles from "app/shared/util/combine-styles";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";
import ActivityComponent from 'app/modules/user-profile/components/activity-component';

interface IActivity extends ITabComponent{
    index: number
}

const useStyles = combineStyles(useTabComponentStyles, makeStyles( (theme: Theme) => ({
})));

const Activity: React.SFC<IActivity> = (props: IActivity) => {
    const tabContext = useContext(TabContext);

    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={props.index !== tabContext.currentTab ? classes.hidden : classes.root}>
            <ActivityComponent 
                url={tabContext.activity.url}
                title="Activities"
            />
        </div>
    )
};

export default Activity;
