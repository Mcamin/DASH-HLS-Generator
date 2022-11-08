import helpers.s3handler as s3



if __name__ == "__main__":
    s3.upload_folder_to_s3(".\\media\\hls\\testmedia", "hls/testmedia")

