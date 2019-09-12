import React from 'react';
import {Tabs, Tab, Paper, makeStyles, Theme} from '@material-ui/core';

interface IUserProfileTabs {
    tabNames: string[],

    handleTabChange(event, value): void
}

const useStyles = makeStyles((theme: Theme) => ({
    root: {
        display: 'flex',
        justifyContent: 'center'
    },
    tab: {
        fontSize: '0.875rem',
        [theme.breakpoints.only('xs')]: {
            fontSize: '0.75rem'
        }
    }
}));

const UserProfileTabs = (props: IUserProfileTabs) => {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
    const classes = useStyles();
    return (
        <Paper square className={classes.root}>
            <Tabs
                value={value}
                indicatorColor="primary"
                textColor="primary"
                onChange={handleChange}
                aria-label="user-profile-tab"
            >
                {props.tabNames.map((tabName, index) =>
                    <Tab
                        key={String(index)}
                        label={tabName}
                        className={classes.tab}
                    />
                )}
            </Tabs>
        </Paper>
    )
};

export default UserProfileTabs;