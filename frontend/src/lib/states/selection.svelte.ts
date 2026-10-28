export class SelectionState {
    selectedIds = $state<string[]>([]);
    isManualMode = $state(false);

    isSelectionMode = $derived(this.isManualMode || this.selectedIds.lenght > 0);

    toggleManual(){
        this.isManualMode = !this.isManualMode;
        if(!this.isManualMode){
            this.selectedIds = [];
        }
    }

    toggle(photoId: string){
        if(this.selectedIds.includes(photoId)){
            this.selectedIds = this.selectedIds.filter(id => id !== photoId);
        } else {
            this.selectedIds.push(photoId);
        }
    }

    cancel(){
        this.selectedIds = [];
        this.isManualMode = false;
    }
    clear(){
        this.selectedIds = [];
    }
    selectSingle(photoId: string){
        this.selectedIds = [photoId];
    }
}