import transform_step

#mcdwt.MCDWT('test_images/','/tmp/',5,1)
transform_step.MCDWT('/tmp/eq/','/tmp/',5,1)
transform_step.iMCDWT('/tmp/','/tmp/res',5,1)

