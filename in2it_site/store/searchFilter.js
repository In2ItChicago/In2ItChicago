export const state = () => ({
    searchFilter: {
        zipOrNeighborhood: '',
        searchRadius: 10,
        startDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
        endDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate())
    }
})