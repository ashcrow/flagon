
from . import TestCase, make_logger

from flagon import errors
from flagon.feature import Feature
from flagon.backends.localmemory import LocalMemoryBackend


class TestFeature(TestCase):

    def setUp(self):
        """
        Set up some items we can reuse.
        """
        self.backend = LocalMemoryBackend(
            {'on': {'active': True}, 'off': {'active': False}})
        self.logger = make_logger()

    def test_feature_manager_creation(self):
        """
        Verify the inputs to Feature and that it is callable.
        """
        feature = Feature(self.backend, self.logger)
        assert callable(feature)
        self.assertRaises(TypeError, Feature)
        self.assertRaises(TypeError, Feature, self.backend)
        self.assertRaises(TypeError, Feature, self.logger)

    def test_feature_decorator(self):
        """
        Test normal usage of the feature decorator.
        """
        feature = Feature(self.backend, self.logger)

        @feature('on')
        def test(a):
            return a

        # This should work
        assert test('1') == '1'

        @feature('off')
        def test2(a):
            return a

        # This should raise a NameError
        self.assertRaises(NameError, test2, '1')

        @feature('off', default=lambda s: "from default")
        def test3(a):
            return a

        # The default should return for this one as it's off and
        # a default is set
        assert test3('1') == "from default"

        # If a feature is attempted that does not exist then it should
        # raise errors.UnknownFeatureError upon definition
        self.assertRaises(
            errors.UnknownFeatureError, feature, test, 'doesntexist')

    def test_feature_is_active(self):
        """
        Verify feature.is_active returns proper information.
        """
        feature = Feature(self.backend, self.logger)
        assert feature.is_active('on')
        assert False == feature.is_active('off')
