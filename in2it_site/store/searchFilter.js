export const state = () => ({
    startTime: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
    endTime: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate() + 7),
    miles: 3,
    address: '60647',
    keywords: '',
    neighborhood: '',
    limit: 4,
    offset: 0
})

export const mutations = {
    set (state, data) {
        state.startTime = data.startTime;
        state.endTime = data.endTime;
        state.miles = data.miles;
        state.address = data.address;
        state.keywords = data.keywords;
        state.neighborhood = data.neighborhood;
        state.limit = data.limit;
        state.offset = data.offset;

        //Miles doesn't apply without a valid origin address
        if(!state.address || state.address.length <= 0){
            state.miles = null;
        }
    },

    setOffset (state, pageNumber) {
        state.offset = (pageNumber - 1) * state.limit;
    }
}