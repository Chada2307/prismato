class SearchState {

    query = $state('');
    
    clear() {
        this.query = '';
    }
}

export const searchState = new SearchState();