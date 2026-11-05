import { PUBLIC_API_URL } from '$env/static/public';
import { invalidateAll } from '$app/navigation';

class UploadManager {
    isUploading = $state(false);
    totalFiles = $state(0);
    uploadedFiles = $state(0);
    errorCount = $state(0);
    isMinimized = $state(false);

    async startUpload(files: File[]) {
        if (files.length === 0) return;

        this.isUploading = true;
        this.totalFiles += files.length;
    
        const BATCH_SIZE = 10;

        for (let i = 0; i < files.length; i += BATCH_SIZE) {

            const batch = files.slice(i, i + BATCH_SIZE);
            const formData = new FormData();

            batch.forEach(file => {
                formData.append('files', file);
            });

            try {
                const res = await fetch(`${PUBLIC_API_URL}/photos/upload/`, {
                    method: 'POST',
                    body: formData
                });

                if (res.ok) {

                    this.uploadedFiles += batch.length;
                } else {
                    this.errorCount += batch.length;
                }
            } catch (error) {
                this.errorCount += batch.length;
            }
        }

        await new Promise(resolve => setTimeout(resolve, 3000));
        await invalidateAll();

        this.isUploading = false;
        this.totalFiles = 0;
        this.uploadedFiles = 0;
        this.errorCount = 0;
    }
}
export const uploader = new UploadManager();