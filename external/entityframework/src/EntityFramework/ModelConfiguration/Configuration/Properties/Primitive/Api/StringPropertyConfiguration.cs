// Copyright (c) Microsoft Open Technologies, Inc. All rights reserved. See License.txt in the project root for license information.

namespace System.Data.Entity.ModelConfiguration.Configuration
{
    using System.ComponentModel.DataAnnotations.Schema;

    /// <summary>
    ///     Used to configure a <see cref="T:System.string" /> property of an entity type or complex type.
    ///     This configuration functionality is available via the Code First Fluent API, see <see cref="DbModelBuilder" />.
    /// </summary>
    public class StringPropertyConfiguration : LengthPropertyConfiguration<Properties.Primitive.StringPropertyConfiguration>
    {
        internal StringPropertyConfiguration(Properties.Primitive.StringPropertyConfiguration configuration)
            : base(configuration)
        {
        }

        /// <summary>
        ///     Configures the property to allow the maximum length supported by the database provider.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsMaxLength()
        {
            base.IsMaxLength();

            return this;
        }

        /// <summary>
        ///     Configures the property to have the specified maximum length.
        /// </summary>
        /// <param name="value"> The maximum length for the property. Setting 'null' will remove any maximum length restriction from the property and a default length will be used for the database column.. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration HasMaxLength(int? value)
        {
            base.HasMaxLength(value);

            Configuration.IsUnicode = Configuration.IsUnicode ?? true;

            return this;
        }

        /// <summary>
        ///     Configures the property to be fixed length.
        ///     Use HasMaxLength to set the length that the property is fixed to.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsFixedLength()
        {
            base.IsFixedLength();

            return this;
        }

        /// <summary>
        ///     Configures the property to be variable length.
        ///     <see cref="T:System.string" /> properties are variable length by default.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsVariableLength()
        {
            base.IsVariableLength();

            return this;
        }

        /// <summary>
        ///     Configures the property to be optional.
        ///     The database column used to store this property will be nullable.
        ///     <see cref="T:System.string" /> properties are optional by default.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsOptional()
        {
            base.IsOptional();

            return this;
        }

        /// <summary>
        ///     Configures the property to be required.
        ///     The database column used to store this property will be non-nullable.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsRequired()
        {
            base.IsRequired();

            return this;
        }

        /// <summary>
        ///     Configures how values for the property are generated by the database.
        /// </summary>
        /// <param name="databaseGeneratedOption"> The pattern used to generate values for the property in the database. Setting 'null' will remove the database generated pattern facet from the property. Setting 'null' will cause the same runtime behavior as specifying 'None'. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration HasDatabaseGeneratedOption(
            DatabaseGeneratedOption? databaseGeneratedOption)
        {
            base.HasDatabaseGeneratedOption(databaseGeneratedOption);

            return this;
        }

        /// <summary>
        ///     Configures the property to be used as an optimistic concurrency token.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsConcurrencyToken()
        {
            base.IsConcurrencyToken();

            return this;
        }

        /// <summary>
        ///     Configures whether or not the property is to be used as an optimistic concurrency token.
        /// </summary>
        /// <param name="concurrencyToken"> Value indicating if the property is a concurrency token or not. Specifying 'null' will remove the concurrency token facet from the property. Specifying 'null' will cause the same runtime behavior as specifying 'false'. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration IsConcurrencyToken(bool? concurrencyToken)
        {
            base.IsConcurrencyToken(concurrencyToken);

            return this;
        }

        /// <summary>
        ///     Configures the name of the database column used to store the property.
        /// </summary>
        /// <param name="columnName"> The name of the column. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration HasColumnName(string columnName)
        {
            base.HasColumnName(columnName);

            return this;
        }

        /// <summary>
        ///     Configures the data type of the database column used to store the property.
        /// </summary>
        /// <param name="columnType"> Name of the database provider specific data type. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration HasColumnType(string columnType)
        {
            base.HasColumnType(columnType);

            return this;
        }

        /// <summary>
        ///     Configures the order of the database column used to store the property.
        ///     This method is also used to specify key ordering when an entity type has a composite key.
        /// </summary>
        /// <param name="columnOrder"> The order that this column should appear in the database table. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public new StringPropertyConfiguration HasColumnOrder(int? columnOrder)
        {
            base.HasColumnOrder(columnOrder);

            return this;
        }

        /// <summary>
        ///     Configures the property to support Unicode string content.
        /// </summary>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public StringPropertyConfiguration IsUnicode()
        {
            IsUnicode(true);

            return this;
        }

        /// <summary>
        ///     Configures whether or not the property supports Unicode string content.
        /// </summary>
        /// <param name="unicode"> Value indicating if the property supports Unicode string content or not. Specifying 'null' will remove the Unicode facet from the property. Specifying 'null' will cause the same runtime behavior as specifying 'false'. </param>
        /// <returns> The same StringPropertyConfiguration instance so that multiple calls can be chained. </returns>
        public StringPropertyConfiguration IsUnicode(bool? unicode)
        {
            Configuration.IsUnicode = unicode;

            return this;
        }
    }
}
