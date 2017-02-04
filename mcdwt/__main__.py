import transform_step

#mcdwt.MCDWT('test_images/','/tmp/',5,1)
transform_step.forward('/tmp/eq/','/tmp/',5,1)
transform_step.backward('/tmp/','/tmp/res',5,1)

