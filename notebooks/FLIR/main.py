from FLIRFlea3 import *

num_frames = 4


def main():
    cam = FLIRFlea3()
    cam.SetAcquisitionControl('AcquisitionMode', 'MultiFrame')
    cam.SetAcquisitionControl('AcquisitionFrameCount', num_frames)
    cam.SetAcquisitionControl('ExposureAuto', 'Continuous')
    cam.PrintNodeValues()
    cam.BeginCapture()
    fig, axs = plt.subplots(nrows=2, ncols=2)
    im = []
    for i in range(num_frames):
        im.append(cam.GetImage())
    cam.EndCapture()

    axs[0][0].imshow(im[0])
    axs[0][1].imshow(im[1])
    axs[1][0].imshow(im[2])
    axs[1][1].imshow(im[3])

    plt.show()

    cam.cam.DeInit()


main()
