Simple python app to interact with AWS MediaConvert.

Converts file from S3 bucket to MP4 or HLS and puts back in same bucket.

Create config locally with the following:

// config.json   
{   
"ENDPOINT_URL": "call describe_endpoint() on MediaConvert client",   
"MP4_PRESET": "presets/aws_mp4_preset_v2.json",   
"HLS_PRESET": "presets/aws_hls_preset.json",   
"MEDIACONVERT_ROLE": "create IAM role in aws",  
"INPUT_BUCKET": "s3://{your-bucket}/{folder}/",  
"OUTPUT_BUCKET": "s3://{your-bucket}/{folder}/",  
"S3_ACCESS_KEY": "bucket access key", //Create input and output if separate  
"S3_SECRET_KEY": "bucket secret key",  
}  
