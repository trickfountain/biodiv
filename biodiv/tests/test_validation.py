from biodiv.validation import det_benchmark, cnts_benchmark
from biodiv.detection import V1
import pytest


class TestCnts_benchmark():
    @pytest.mark.parametrize(
        "img_src,results_dic",
        [
            ('biodiv/tests/test_images/five_shapes_lab.png',
                {'recall': 100,
                 'precision': 100,
                 'tot_matches': 5,
                 'un_matches': 5,
                 'tot_targets': 5,
                 'tot_cnts': 5}),
            ('biodiv/tests/test_images/three_drawings_lab.png',
                {'recall': 100,
                 'precision': 100,
                 'tot_matches': 3,
                 'un_matches': 3,
                 'tot_targets': 3,
                 'tot_cnts': 3}),
            ]
        )
    def test_shapes(self, img_src, results_dic):
        '''Test detection with easy samples.
        Expecting an exact match
        '''

        results = cnts_benchmark(img_src)

        assert results == results_dic

    @pytest.mark.parametrize("img_src,img_lab,min_recall,min_precision",
        [('biodiv/tests/test_images/but1.jp2',
          'biodiv/tests/test_images/but1_lab.jp2',
           0.5, 0.5),
         ('biodiv/tests/test_images/cats1.jp2',
          'biodiv/tests/test_images/cats1_lab.jp2',
           0.5, 0.5)
           ])
    def test_samples_V1(self, img_src, img_lab, min_recall, min_precision):
        '''Test series of real example and insure
        adequate precision and recall metrics.
        '''

        results = det_benchmark(img_src, img_lab, detector=V1)
        recall = results['recall'] > min_recall
        precision = results['precision'] > min_precision

        assert recall and precision
