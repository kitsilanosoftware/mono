//------------------------------------------------------------------------------
// <auto-generated>
//    This code was generated from a template.
//
//    Manual changes to this file may cause unexpected behavior in your application.
//    Manual changes to this file will be overwritten if the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace FunctionalTests.ProductivityApi.TemplateModels.CsMonsterModel
{
    using System;
    using System.Collections.Generic;
    
    public partial class ProductWebFeatureMm
    {
        public int FeatureId { get; set; }
        public Nullable<int> ProductId { get; set; }
        public Nullable<int> PhotoId { get; set; }
        public int ReviewId { get; set; }
        public string Heading { get; set; }
    
        public virtual ProductReviewMm Review { get; set; }
        public virtual ProductPhotoMm Photo { get; set; }
    }
}
