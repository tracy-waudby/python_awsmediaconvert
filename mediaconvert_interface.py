import json
import boto3

#https://docs.aws.amazon.com/mediaconvert/latest/apireference/getting-started.html

#1 Create MediaConvret IAM role to get access keys
#2 describe_endpoint() to get endpoint URL 
#3 Create presets


class S3Interface():

   # S3_ACCESS_KEY= config["S3_ACCESS_KEY"]
   # S3_SECRET_KEY= config["S3_SECRET_KEY"]
   pass


class MediaConvertInterface():
   
    def __init__(self):
        config = {}
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.MP4_preset = config["MP4_PRESET"]
        self.HLS_preset = config["HLS_PRESET"]
        self.role = config["MEDIACONVERT_ROLE"]
        self.input = config["INPUT_BUCKET"]
        self.output = config["OUTPUT_BUCKET"]
        self.mediaconvert_client = boto3.client('mediaconvert', 
                                endpoint_url=config["ENDPOINT_URL"], 
                                aws_access_key_id=config["S3_ACCESS_KEY"],
                                aws_secret_access_key=config["S3_SECRET_KEY"],
                                region_name='us-east-1')
     


    def create_job(self, file, video_type="HLS"):

        if video_type == "HLS":
            preset_config = self.HLS_preset
        if video_type == "MP4":
            preset_config =self.MP4_preset
        else:
            return "Invalid preset type. MP4 or HLS allowed." 

        with open(preset_config, "r") as jsonfile:
            job_object = json.load(jsonfile)

        job_object["Role"] = self.role
        job_object["Settings"]["Inputs"][0]["FileInput"] = self.input + file

        if video_type == "HLS":
            job_object["Settings"]["OutputGroups"][0]["OutputGroupSettings"]["HlsGroupSettings"]["Destination"] = self.output
        elif video_type == "MP4":
            job_object["Settings"]["OutputGroups"][0]["OutputGroupSettings"]["FileGroupSettings"]["Destination"] = self.output


        response = self.mediaconvert_client.create_job(**job_object)
        job_id = response["Job"]["Id"]
        return job_id


    def job_status(self, job_id):

        job = self.mediaconvert_client.get_job(Id=job_id)
    
        # 'SUBMITTED'|'PROGRESSING'|'COMPLETE'|'CANCELED'|'ERROR'
        status = job["Job"]["Status"]

        error=""
        try:
            error = job["Job"]["ErrorMessage"]
        except KeyError:
            error = "No error message returned"

        return status, error 


