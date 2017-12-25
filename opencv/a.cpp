#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/stitching/detail/seam_finders.hpp>
#include <iostream>

using namespace cv;
using namespace cv::detail;

int main()
{
    Mat image1 = imread("duck.jpg");
    Mat image2 = imread("duck.jpg");
    image1.convertTo(image1, CV_32FC3, 1/255.0);
    image2.convertTo(image2, CV_32FC3, 1/255.0);

    std::vector<Mat> sources;
    sources.push_back(image1);
    sources.push_back(image2);

    std::vector<Point> corners;
    corners.push_back(Point(0, 0));
    corners.push_back(Point(300, 0));

    std::vector<Mat> masks;
    masks.push_back(Mat(image1.size(), CV_8U, Scalar(255)));
    masks.push_back(Mat(image2.size(), CV_8U, Scalar(255)));

    // Ptr<SeamFinder> seam_finder = new GraphCutSeamFinder(GraphCutSeamFinderBase::COST_COLOR, 0.1, 30);
    Ptr<SeamFinder> seam_finder = new GraphCutSeamFinder();
    seam_finder->find(sources, corners, masks);

    int gap = 2;
    Mat canvas(image2.rows, image2.cols + 300 + gap, CV_32FC3);
    canvas.setTo(0);
    image1.copyTo(canvas(Range::all(), Range(0, image1.cols)), masks[0]);
    image2.copyTo(canvas(Range::all(), Range(300 + gap, image2.cols + 300 + gap)), masks[1]);

    imshow("canvas",canvas);
    waitKey(0);

    return 0;
}
