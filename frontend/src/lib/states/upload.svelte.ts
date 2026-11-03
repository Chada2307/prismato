import { PUBLIC_API_URL } from '$env/static/public';
import { invalidateAll } from '$app/navigation';

class UploadManager{
    isUploading = $state(false);
    totalFiles = $state(0);
    uploadedFiles = $state(0);
    errorCount = $state(0);
    isMinimized = $state(false);

    async startUpload(files: File[]){
        if(files.length === 0) return;

        this.isUploading = true;
        this.totalFiles += files.length;

        for(let i = 0; i < files.length; i++){
            const formData = new FormData();
            formData.append('file', files[i]);

            try{
                const res = await fetch(`${PUBLIC_API_URL}/photos/upload/`, {
                    method: 'POST',
                    body: formData
                });

                if (res.ok){
                    this.uploadedFiles++;
                }else{
                    this.errorCount++;
                }
            }catch(error){
                this.errorCount++;
            }
        }

        await invalidateAll();

        setTimeout(() => {
            this.isUploading = false;
            this.totalFiles = 0;
            this.uploadedFiles = 0;
            this.errorCount = 0;
        }, 3000);
    }
}
export const uploader = new UploadManager();