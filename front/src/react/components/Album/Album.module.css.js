const styles = theme => ({
    card: {
        maxWidth: 250,
    },
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    playIcon: {
        height: 35,
        width: 35,
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    }
});

export default styles;
