import request from "@/utils/request";

const API_PATH = "/common/file";

const AuthAPI = {
    upload(body: FormData) {
        return request<ApiResponse<UploadResult>>({
            url: `${API_PATH}/upload`,
            method: "post",
            headers: {
                "Content-Type": "multipart/form-data",
            },
            data: body,
        });
    },
    download(body:DownloadBody) {
        return request<ApiResponse<string>>({
            url: `${API_PATH}/download`,
            method: "post",
            data: body,
        });
    },
};

export default AuthAPI;

export interface DownloadBody {
    file_path: string;
    delete:boolean
}
export interface UploadResult {
    file_url: string;
    file_name: string;
}